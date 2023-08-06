"""
httpx.Client
"""
import httpx
from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
time = LazyLoader("time", globals())
warnings = LazyLoader("warnings", globals())

utils = LazyLoader("utils", globals(), "pyxk.utils")
console = LazyLoader("console", globals(), "rich.console")
progress = LazyLoader("progress", globals(), "rich.progress")



class Client(httpx.Client):
    """httpx.Client 重构"""

    def __init__(self, **kwargs):

        # 允许请求重定向
        follow_redirects = kwargs.pop("follow_redirects", True)

        # 配置默认 User-Agent
        headers = httpx.Headers(
            dict( kwargs.pop("headers", None) or {} )
        )
        headers.setdefault("user-agent", utils.UA_ANDROID)

        kwargs.__setitem__("follow_redirects", follow_redirects)
        kwargs.__setitem__("headers", headers)
        super().__init__(**kwargs)

        self._console = console.Console()


    def send(self, request, **kwargs):

        exc_count, exc_max = {}, 10
        while True:
            try:
                with self._console.status(f"[magenta b]Send Request[/]: {str(request.url)}"):
                    response = super().send(request, **kwargs)
                break

            # 请求超时
            except httpx.ConnectTimeout as exc:
                reason  = exc.args[0]
                timeout = request.extensions["timeout"]["connect"]
                warnings.warn(
                    f"{reason!r}: {timeout}, url: {str(request.url)!r}",
                )
                # except 计数
                exc_count.setdefault(reason, 0)
                exc_count[reason] += 1
                if exc_count[reason] >= exc_max:
                    raise
                time.sleep(1)

            # 无网络连接
            except httpx.ConnectError as exc:
                reason = exc.args[0]
                reason_re = ("[Errno 7]", )
                reason_ok = lambda : True in [reason.startswith(item) for item in reason_re]

                if not reason_ok():
                    raise
                warnings.warn(
                    "请检查网络连接是否正常...",
                )
                time.sleep(1)

        return response


    def wget(
        self,
        url,
        method="GET",
        *,
        content=None,
        data=None,
        files=None,
        json=None,
        params=None,
        headers=None,
        cookies=None,
        auth=None,
        follow_redirects=True,
        timeout=5,
        extensions=None,
        file=None,
        resume=False
    ):
        """ 流式响应 大体积文件下载 """
        # 获取完整文件路径
        filepath, filename = os.path.split(
            os.path.abspath(file or utils.hash256(url))
        )
        if len(filename.rsplit(".", 1)) == 1:
            try:
                response = self.head(
                    url=url,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions
                )
                suffix = response.headers.get("content-type", None)
                if suffix:
                    suffix = "." + suffix.split("/", 1)[-1].split(";", 1)[0]
                else:
                    suffix = ""
            except Exception:
                suffix = ""
            filename += suffix
        file = os.path.join(filepath, filename)
        del filepath, filename

        # 断点续传 获取本地文件大小
        filesize, chunksize, filemode = 0, 1024, "wb"

        if resume and os.path.isfile(file):
            filesize, filemode = os.path.getsize(file), "ab"
            headers = httpx.Headers( dict(headers or {}) )
            headers["range"] = f"bytes={filesize}-"

        # 开启 流式响应
        with self.stream(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
        ) as response:

            if response.status_code == 416:
                # self._console.print(f"complete: [bright_blue]{file}[/]")
                return response

            with progress.Progress(
                *(
                    progress.SpinnerColumn("line"),
                    progress.TextColumn("[progress.description]{task.description}"),
                    progress.BarColumn(finished_style="green"),
                    progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                    progress.TimeElapsedColumn()
                ),
                console=self._console,
                transient=True
            ) as _progress:

                content_length = response.headers.get("content-length", None)
                task = _progress.add_task(
                    description = "[magenta b]downloading[/]",
                    total = None if content_length is None else filesize + int(content_length)
                )
                _progress.update(task, advance=filesize)

                with utils.open(file, filemode) as fileobj:
                    for chunk in response.iter_bytes(chunksize):
                        fileobj.write(chunk)
                        _progress.update(task, advance=chunksize)

                # self._console.print(f"complete: [bright_blue]{file}[/]")
                return response
