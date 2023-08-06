import requests
from requests.structures import CaseInsensitiveDict

from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
time = LazyLoader("time", globals())
_parse = LazyLoader("_parse", globals(), "urllib.parse")
warnings = LazyLoader("warnings", globals())

console = LazyLoader("console", globals(), "rich.console")
progress = LazyLoader("progress", globals(), "rich.progress")
utils = LazyLoader("utils", globals(), "pyxk.utils")



class Session(requests.Session):
    """requests.Session 重构"""

    def __init__(self, base_url=None):

        super().__init__()
        self.headers["User-Agent"] = utils.UA_ANDROID
        self._base_url = base_url if isinstance(base_url, str) else ""
        self._console  = console.Console()

    @property
    def base_url(self):
        return getattr(self, "_base_url", None) or ""

    @base_url.setter
    def base_url(self, _url):
        if not isinstance(_url, str):
            raise TypeError(
                f"base_url 必须是 'str' 类型, got {type(_url).__name__!r}"
            )
        self._base_url = _url

    @staticmethod
    def _is_absolute_url(_url, /):
        _url = _parse.urlsplit(_url)
        return bool(_url.scheme and _url.netloc)

    def _build_url(self, _url, /):
        if self._is_absolute_url(_url):
            return _url
        return _parse.urljoin(self.base_url, _url)


    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=5,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None
    ):
        exc_count, exc_max = {}, 10
        url = self._build_url(url)
        while True:
            try:
                with self._console.status(f"[magenta b]Send Request[/]: {url}"):
                    response = super().request(
                        method=method,
                        url=url,
                        params=params,
                        data=data,
                        headers=headers,
                        cookies=cookies,
                        files=files,
                        auth=auth,
                        timeout=timeout,
                        allow_redirects=allow_redirects,
                        proxies=proxies,
                        hooks=hooks,
                        stream=stream,
                        verify=verify,
                        cert=cert,
                        json=json,
                    )
                break

            except requests.exceptions.Timeout:

                reason = "timeout:" + url
                warnings.warn(
                    f"timeout: {timeout}, url: {(url)!r}",
                )
                # except 计数
                exc_count.setdefault(reason, 0)
                exc_count[reason] += 1
                if exc_count[reason] >= exc_max:
                    raise
                time.sleep(1)

            except requests.exceptions.ConnectionError as exc:

                reason = str(exc.args[0])
                reason_re = ("[Errno 7]", )
                reason_ok = lambda : True in [item in reason for item in reason_re]

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
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=5,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        verify=None,
        cert=None,
        json=None,
        file=None,
        resume=False
    ):
        """ 流式响应 大体积文件下载 """
        if not isinstance(file, str):
            if file is not None:
                warnings.warn(
                    f"{self.__class__.__name__}.wget 参数 'file' 必须是 'str' 类型, "
                    f"got {type(file).__name__!r}"
                )
            file = utils.hash256(url)

        # 获取完整文件路径
        filepath, filename = os.path.split(
            os.path.abspath(file or utils.hash256(url))
        )
        if len(filename.rsplit(".", 1)) == 1:
            try:
                response = self.head(
                    url=url,
                    params=params,
                    data=data,
                    headers=headers,
                    cookies=cookies,
                    files=files,
                    auth=auth,
                    timeout=timeout,
                    allow_redirects=allow_redirects,
                    proxies=proxies,
                    hooks=hooks,
                    stream=False,
                    verify=verify,
                    cert=cert,
                    json=json
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
            headers = CaseInsensitiveDict( dict(headers or {}) )
            headers["Range"] = f"bytes={filesize}-"

        # 开启流式响应
        response = self.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=True,
            verify=verify,
            cert=cert,
            json=json
        )

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
                for chunk in response.iter_content(chunksize):
                    fileobj.write(chunk)
                    _progress.update(task, advance=chunksize)

            # self._console.print(f"complete: [bright_blue]{file}[/]")
        return response
