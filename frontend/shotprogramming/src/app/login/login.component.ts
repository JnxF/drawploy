import {AfterViewInit, Component, NgZone} from '@angular/core';
import {ApiService} from "../api/api.service";
import {Router} from "@angular/router";

declare const gapi: any;

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements AfterViewInit {
  public auth2: any;

  private _isMouseIn = false;

  get isMouseIn(): boolean {
    return this._isMouseIn;
  }

  public mouseIn() {
    this._isMouseIn = true;
  }

  public mouseOut() {
    this._isMouseIn = false;
  }

  public googleInit() {
    if (window['gapi']) {
      gapi.load('auth2', () => {
        this.auth2 = gapi.auth2.init({
          client_id: '1075282744065-e9a4npkj3o82anu7ufii4av0u5c1v53b.apps.googleusercontent.com',
          cookiepolicy: 'single_host_origin',
          scope: 'profile email https://www.googleapis.com/auth/cloud-platform'
        });
        this.attachSignin(document.getElementById('googleBtn'));
      });
    } else {
      setTimeout(this.googleInit.bind(this), 1);
    }
  }



  public attachSignin(element) {
    this.auth2.attachClickHandler(element, {},
      (googleUser) => {
        this._api.googleUser = googleUser;
        this._ngZone.run(() => this._router.navigate(['home']).then());
      }, (error) => {
        console.error(error);
      });
  }

  constructor(private _api: ApiService, private _router: Router, private _ngZone: NgZone) {
  }

  ngAfterViewInit(): void {
    this.googleInit();
  }
}
