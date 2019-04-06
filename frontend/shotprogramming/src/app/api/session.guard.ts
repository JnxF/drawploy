import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree} from "@angular/router";
import {Observable} from "rxjs";
import {ApiService} from "./api.service";

@Injectable({
  providedIn: 'root'
})
export class SessionGuard implements CanActivate {
  constructor(private _router: Router, private _api: ApiService) {
  }

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot):
    Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    console.log(this._api.googleUser);
    if (this._api.googleUser != null) {
      return true;
    }
    this._router.navigate(['login']).then();
    return false;
  }
}
