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

  public googleUser: any;

  public get options(): any {
    return {
      observe: 'body',
      params: {token: this.userToken, email: this.userEmail}
    };
  }

  public get userEmail(): string {
    return this.googleUser.getBasicProfile().getEmail();
  }

  public get userToken(): string {
    return this.googleUser.getAuthResponse().access_token;
  }

  constructor(private _http: HttpClient) {
  }

  public static sCompleteUrl(url: string): string {
    return new URL(url, this._sApiUrl).toString();
  }

  public get<T>(relativeUrl: string, instantiateClass?: Type<T>, params?: any): Observable<T> {
    const options = Object.assign({}, this.options);
    options.params = params ? Object.assign({}, this.options.params, params) :
      Object.assign({}, this.options.params);
    const myPipe = this._http.get(ApiService.sCompleteUrl(relativeUrl), options) as Observable<any>;
    if (instantiateClass) {
      myPipe.pipe(
        map(obj => new instantiateClass(obj))
      );
    }
    return myPipe as Observable<T>;
  }

  public post<P, R>(relativeUrl: string, object: any, instantiateClass?: Type<R>): Observable<R> | Observable<P> {
    const myPipe = this._http.post(ApiService.sCompleteUrl(relativeUrl), object, this.options);
    if (instantiateClass) {
      myPipe.pipe(
        map(obj => new instantiateClass(obj))
      );
    }
    return myPipe as Observable<any>;
  }
}
