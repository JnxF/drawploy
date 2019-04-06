import {Injectable, Type} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private static readonly _sApiUrl = environment.apiUrl;

  constructor(private _http: HttpClient) {
  }

  public static sCompleteUrl(url: string): string {
    return new URL(url, this._sApiUrl).toString();
  }

  public post<P, R>(relativeUrl: string, object: any, instantiateClass?: Type<R>): Observable<R>|Observable<P> {
    const myPipe = this._http.post(ApiService.sCompleteUrl(relativeUrl), object, {
      observe: 'body'
    });
    if (instantiateClass) {
      myPipe.pipe(
        map(obj => new instantiateClass(obj))
      );
    }
    return myPipe as Observable<any>;
  }
}
