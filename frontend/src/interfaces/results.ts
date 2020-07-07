export interface IResultError {
  error: IResultErrorArray;
}

export interface IResultErrorArray {
  reason: string;
  url: string;
}

export interface IResultSuccess {
  id: number;
  hop: number;
  url: string;
  http_version: string;
  status_code: IStatusCode;
  headers: object;
  host: string;
  path: string;
  scheme: string;
  ipaddr: string;
  time_elapsed: number;
}

export interface IStatusCode {
  code: string;
  phrase: string;
}
