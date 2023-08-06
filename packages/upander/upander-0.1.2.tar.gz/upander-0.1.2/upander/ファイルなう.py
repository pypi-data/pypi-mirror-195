from upander import Uploader
from upander import UploaderPoster
from upander import UploaderPosterResponse
from upander import UploaderDownloader
from upander import UploaderDownloaderResponse

import requests 
from urllib.parse import urlparse
from typing import Optional, IO,  List, TypedDict, Literal
import datetime
import re
import time
import dataclasses

class ファイルなう(Uploader):
  UPLOAD_FILE_SIZE_LIMIT = 8 * 1024 * 1024 * 1024
  TIME_LIMIT = {
    "10M": 10 * 60,
    "30M": 30 * 60,
    "01H":  1 * 60 * 60,
    "02H":  2 * 60 * 60,
    "03H":  3 * 60 * 60,
    "06H":  6 * 60 * 60,
    "12H": 12 * 60 * 60,
    "01D":  1 * 60 * 60 * 24,
    "02D":  2 * 60 * 60 * 24,
    "03D":  3 * 60 * 60 * 24,
    "05D":  5 * 60 * 60 * 24,
    "07D":  7 * 60 * 60 * 24,
    "10D": 10 * 60 * 60 * 24,
    "15D": 15 * 60 * 60 * 24,
    "20D": 20 * 60 * 60 * 24,
    "30D": 30 * 60 * 60 * 24,
  }
  DOMEIN = '.kuku.lu'

  def DeleteList(url: str, cookies: dict, delete_only_list=False, session: requests.Session = None) -> requests.Response:
    if delete_only_list:
      return ファイルなう.Delete(url, cookies, session)

    __hash = url.split("/")[-1]
    headers = {
        'authority': 'd.kuku.lu',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ja',
        'referer': 'https://d.kuku.lu'+__hash,
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
    }
    params = {
        'action': 'delete',
        'delete_linkfile': '1',
        'hash': __hash,
    }
    return requests.get('https://d.kuku.lu/view.php', params=params, cookies=cookies, headers=headers)

  def RegList(url_list: list, cookies: dict, password: str = None, session: requests.Session = None) -> requests.Response:
    __hash_list = [url.split("/")[-1] for url in url_list]
    headers = {
        'authority': 'd.kuku.lu',
        'accept': '*/*',
        'accept-language': 'ja',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://d.kuku.lu',
        'referer': 'https://d.kuku.lu/upload.php?uuid={}&t={}'.format(cookies["cookie_uid"], time),
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = '&action=reglist&ajax=1&uuid={}&link_hash={}'.format(cookies["cookie_uid"], "%2C".join(__hash_list))
    if session is None:
      import requests as _http
    else:
      _http = session
    response = _http.post('https://d.kuku.lu/list.php', cookies=cookies, headers=headers, data=data)
    if password:
      try:
        print(ファイルなう.SetDownloadPassWord("https://d.kuku.lu/"+response.json()["hash"], cookies, password, session).text)
      except Exception as e:
        print(e, response.text)
    return response

  def SetTimelimit(url: str, cookies: dict, timelimit: Literal["10M", "30M", "01H", "02H", "03H", "06H", "12H", "01D", "02D", "03D", "05D", "07D", "10D", "15D", "20D", "30D"], session: requests.Session = None) -> requests.Response:
    if ファイルなう.TIME_LIMIT.get(timelimit, None) is None:
      raise ValueError("timelimit に指定できる値は「'" + "','".join(list(ファイルなう.TIME_LIMIT.keys())) + "'」です。")
    __hash = url.split("/")[-1]
    headers = {
        'authority': 'd.kuku.lu',
        'accept': '*/*',
        'accept-language': 'ja',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://d.kuku.lu',
        'referer': 'https://d.kuku.lu/'+__hash,
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'hash': __hash,
    }
    data = {
        'action': 'addTimelimit',
        'set_timelimit': ファイルなう.TIME_LIMIT[timelimit],
    }
    if session is None:
      import requests as _http
    else:
      _http = session
    return _http.post('https://d.kuku.lu/view.php', params=params, cookies=cookies, headers=headers, data=data)

  def SetDownloadPassWord(url: str, cookies: dict, password: str, session: requests.Session = None) -> requests.Response:
    __hash = url.split("/")[-1]
    headers = {
      'authority': 'd.kuku.lu',
      'accept': '*/*',
      'accept-language': 'ja',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'origin': 'https://d.kuku.lu',
      'referer': 'https://d.kuku.lu/'+__hash,
      'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
      'x-requested-with': 'XMLHttpRequest',
    }
    params = {
      'hash': __hash,
    }
    data = {
      'action': 'setDownloadPassword',
      'set_dlpass': password,
    }

    if session is None:
      import requests as _http
    else:
      _http = session
    return _http.post('https://d.kuku.lu/view.php', params=params, cookies=cookies, headers=headers, data=data)

  def Delete(url: str, cookies: dict, session: requests.Session = None) -> requests.Response:
    __hash = url.split("/")[-1]
    headers = {
        'authority': 'd.kuku.lu',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ja',
        'referer': 'https://d.kuku.lu/{}'.format(__hash),
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41',
    }
    if session is None:
      import requests as _http
    else:
      _http = session
    return _http.get('https://d.kuku.lu/view.php?action=delete&hash={}'.format(__hash), cookies=cookies, headers=headers)

  class Downloader(UploaderDownloader):
    def __init__(self, url: str, password: str=None, cookies: dict=None):
      self.__url = url
      self.__password = password
      if not(cookies is None):
        self.__cookies = cookies
      else:
        self.__cookies = {}

    def download(self) -> Optional[UploaderDownloaderResponse]:
      with requests.Session() as session:
        if self.__cookies.get(ファイルなう.DOMEIN, {}).get("cookie_uid", None) is None:
          self.__regist_cookie_uid(session)
        if self.__password and not(self.__cookies.get(ファイルなう.DOMEIN, {}).get("cookie_dlpassword", None) == self.__url.split("/")[-1]+"%40"+self.__password):
          if not(self.__checkDownloadPassword(session).text == "result=OK;"):
            raise Exception("パスワードが違います。")
        file_direct_url, file_name = self.__getDirectUrl_and_FileName()
        headers = {
          'authority': urlparse(file_direct_url).netloc,
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'accept-language': 'ja',
          'referer': 'https://d.kuku.lu/',
          'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'document',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-site': 'cross-site',
          'sec-fetch-user': '?1',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
        }
      return ファイルなう.Downloader.Response(session.get( file_direct_url, headers=headers ), file_name, self.__cookies)

    def __getDirectUrl_and_FileName(self):
      headers = {
        'authority': 'd.kuku.lu',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ja',
        'cache-control': 'max-age=0',
        'referer': self.__url,
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
      }
      time.sleep(1)
      response = requests.get(self.__url, cookies=self.__cookies[ファイルなう.DOMEIN], headers=headers)
      m1 = re.match("[\s\S]*javascript:downloadDirect\(.(http.+).\)[\s\S]*", response.text)
      m2 = re.match('[\s\S]*<meta property="og:description" content="(.+) \(.+"[\s\S]*', response.text)
      if m1:
        return (m1.groups()[0], m2.groups()[0] )
      else:
        raise Exception("ダウンロードリンクが検出できませんでした。"+"\n\n"+response.text)

    def __checkDownloadPassword(self, session: requests.Session):
      __hash = self.__url.split("/")[-1]
      headers = {
        'authority': 'd.kuku.lu',
        'accept': '*/*',
        'accept-language': 'ja',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://d.kuku.lu',
        'referer': self.__url,
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
        'x-requested-with': 'XMLHttpRequest',
      }
      params = {
        'hash': __hash,
      }
      data = {
        'action': 'checkDownloadPassword',
        'dlpass': self.__password,
      }
      response = requests.post('https://d.kuku.lu/view.php', params=params, cookies=self.__cookies[ファイルなう.DOMEIN], headers=headers, data=data)
      cookies = response.cookies
      for cookie_domein in cookies.list_domains():
        self.__cookies[cookie_domein] = cookies.get_dict(cookie_domein)
      self.__cookies[ファイルなう.DOMEIN]["cookie_dlpassword"] = __hash+"%40"+self.__password
      return response

    def __regist_cookie_uid(self, session: requests.Session):
      cookies = session.get('https://d.kuku.lu/index.php', cookies=None).cookies
      for cookie_domein in cookies.list_domains():
        self.__cookies[cookie_domein] = cookies.get_dict(cookie_domein)

    class Response(UploaderDownloaderResponse):
      def __init__(self, response: requests.Response, file_name: str, cookies):
        self.__dl_file_name = file_name
        self.__status = response.status_code
        self.__url = response.url
        self.__encoding = response.encoding
        self.__headers = response.headers
        self.__content = response.content
        self.__cookies = response.cookies
      def dl_file_name(self) -> str: return self.__dl_file_name
      def status(self) -> int      : return self.__status
      def url(self) -> str         : return self.__url
      def encoding(self) -> str    : return self.__encoding
      def headers(self) -> str     : return self.__headers
      def content(self) -> bytes   : return self.__content
      def cookies(self) -> dict    : return self.__cookies

  class Poster(UploaderPoster):
    PosterRunAllResponse = TypedDict('PosterRunAllResponse', {'uploaded_files_response': List[UploaderPosterResponse], 'reglist_response': Optional[requests.Response], "cookies": dict})

    def __init__(self, settings_list: list, cookies: dict=None):
      self.__settings_list = settings_list
      if not(cookies is None):
        self.__cookies = cookies
      else:
        self.__cookies = {}
      self.__upload_cnt = 0

    def run(self):
      """ファイルのアップロードを行います。
      インスタンス作成時のsettings_list引数に従い処理を行います。一度の呼び出しで、１つのファイルのみをアップロードします。 settings_listの長さが１でない場合、１度の呼び出しで最初の要素から順に処理を行っていきます。 すべてのファイルをアップロードし終えた時に呼び出すと、Noneを返します。
      """
      with requests.Session() as session:
        if self.__cookies.get(ファイルなう.DOMEIN, {}).get("cookie_uid", None) is None:
          self.__regist_cookie_uid(session)

        if len(self.__settings_list) == self.__upload_cnt:
          return None

        settings = self.__settings_list[self.__upload_cnt]
        response = self.__getUploadServerMulti(session)
        if not( response.json().get("result") == "OK" ) : raise Exception(response.text)

        upload_response = self.__upload(session, response.json()["servers"][0], settings.file)
        upload_response = ファイルなう.Poster.Response(upload_response, self.__cookies)

        if settings.password:
          time.sleep(5)
          response = self.__setDownloadPassWord(session, upload_response.dl_url(), settings.password)
        if settings.timelimit:
          time.sleep(5)
          response = self.__setTimeLimit(session, upload_response.dl_url(), settings.timelimit)
        if settings.autoClose:
          settings.file.close()
        self.__upload_cnt = self.__upload_cnt + 1
      return upload_response

    def run_all(self, isRegList=False, list_password: str = None) -> PosterRunAllResponse:
      response_list = []
      for i in range(self.__upload_cnt, len(self.__settings_list)):
        response_list.append( self.run() )
        time.sleep(10)
      reglist_response = None
      if isRegList:
        reglist_response = ファイルなう.RegList([i.dl_url() for i in response_list], self.__cookies[ファイルなう.DOMEIN], list_password)
      return {
        "uploaded_files_response": response_list,
        "reglist_response": reglist_response,
        "cookies": self.__cookies
      }

    def __regist_cookie_uid(self, session: requests.Session):
      cookies = session.get('https://d.kuku.lu/index.php', cookies=None).cookies
      for cookie_domein in cookies.list_domains():
        self.__cookies[cookie_domein] = cookies.get_dict(cookie_domein)

    def __setTimeLimit(self, session: requests.Session, url: str, timelimit: str) -> requests.Response:
      return ファイルなう.SetTimelimit(url, self.__cookies[ファイルなう.DOMEIN], timelimit, session)

    def __setDownloadPassWord(self, session: requests.Session, url:str, password: str) -> requests.Response:
      return ファイルなう.SetDownloadPassWord(url, self.__cookies[ファイルなう.DOMEIN], password, session)

    def __upload(self, session: requests.Session, upload_server, file: IO) -> requests.Response:
      headers = {
          'Accept': '*/*',
          'Accept-Language': 'ja',
          'Connection': 'keep-alive',
          'Origin': 'https://d.kuku.lu',
          'Referer': 'https://d.kuku.lu/',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-site',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41',
          'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
      }
      files = {
          'ajax': (None, '1'),
          'uuid': (None, self.__cookies[ファイルなう.DOMEIN]["cookie_uid"]),
          'country': (None, 'JP'),
          'file_1': file,
          'file_1_name': (None, file.name.split("/")[-1]),
          'file_1_type': (None, 'file'),
          'filecnt': (None, '1'),
      }
      response = session.post('https://{upload_server}/upload.php'.format(upload_server=upload_server), cookies=self.__cookies[ファイルなう.DOMEIN], headers=headers, files=files, verify=False)
      return response

    def __getUploadServerMulti(self, session: requests.Session) -> dict:
      headers = {
        'authority': 'd.kuku.lu',
        'accept': '*/*',
        'accept-language': 'ja',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://d.kuku.lu',
        'referer': 'https://d.kuku.lu/upload.php?uuid={}&t={}'.format(self.__cookies[ファイルなう.DOMEIN]["cookie_uid"], str(int(datetime.datetime.timestamp(datetime.datetime.now())))),
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41',
        'x-requested-with': 'XMLHttpRequest',
      }
      data = {
        'action': 'getUploadServerMulti',
      }
      response = session.post('https://d.kuku.lu/index.php', cookies=self.__cookies[ファイルなう.DOMEIN], headers=headers, data=data)
      return response

    @dataclasses.dataclass(frozen=True)
    class Settings:
      file: IO
      password: str = None
      timelimit: Literal["10M", "30M", "01H", "02H", "03H", "06H", "12H", "01D", "02D", "03D", "05D", "07D", "10D", "15D", "20D", "30D"] = None
      autoClose: bool = True
      def __post_init__(self):
        if not(self.timelimit is None) and ファイルなう.TIME_LIMIT.get(self.timelimit, None) is None:
          raise ValueError("timelimit に指定できる値は「'" + "','".join(list(ファイルなう.TIME_LIMIT.keys())) + "'」です。")

    class Response(UploaderPosterResponse):
      def __init__(self, response: requests.Response, cookies: dict):
        if not( response.text[:response.text.find(":")] == "OK" ) : raise Exception(response.text)
        self.__dl_url = response.text[response.text.find(":")+1:]
        self.__dl_file_name = ""
        self.__status = response.status_code
        self.__url = response.url
        self.__encoding = response.encoding
        self.__headers = response.headers
        self.__text = response.text
        self.__content = response.content
        self.__cookies = cookies
      def dl_url(self) -> str       : return self.__dl_url
      def dl_file_name(self) -> str : return self.__dl_file_name
      def status(self) -> int       : return self.__status
      def url(self) -> str          : return self.__url
      def encoding(self) -> str     : return self.__encoding
      def headers(self) -> str      : return self.__headers
      def text(self) -> str         : return self.__text
      def content(self) -> bytes    : return self.__content
      def cookies(self) -> dict     : return self.__cookies
