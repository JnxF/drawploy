import {AfterViewInit, Component, DoCheck} from '@angular/core';
import {ApiService} from "../api/api.service";
import {Router} from "@angular/router";

declare const gapi: any;

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements AfterViewInit, DoCheck {
  public auth2: any;

  public googleInit() {
    gapi.load('auth2', () => {
      this.auth2 = gapi.auth2.init({
        client_id: '1075282744065-e9a4npkj3o82anu7ufii4av0u5c1v53b.apps.googleusercontent.com',
        cookiepolicy: 'single_host_origin',
        scope: 'profile email'
      });
      this.attachSignin(document.getElementById('googleBtn'));
    });
  }

  public attachSignin(element) {
    this.auth2.attachClickHandler(element, {},
      (googleUser) => {
        this._api.googleUser = googleUser;
      }, (error) => {
        console.error(error);
      });
  }

  constructor(private _api: ApiService, private _router: Router) {
  }

  ngDoCheck(): void {
    if (this._api.googleUser != null) {
      this._router.navigate(['home']).then();
    }
  }

  ngAfterViewInit(): void {
    this.googleInit();
  }
}
