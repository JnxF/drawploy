import {Component, NgZone} from '@angular/core';
import {ApiService} from "./api/api.service";
import {Router} from "@angular/router";

declare const gapi: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  private _timeout: any;
  private _count: number = 0;

  constructor(public api: ApiService,
              private _router: Router,
              private _ngZone: NgZone) {
  }

  public emailClick() {
    this._count++;
    if (this._count > 10) {
      clearTimeout(this._timeout);
      this._timeout = setTimeout(() => this._finish(), 500);
    }
  }

  public signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(() => {
      this.api.googleUser = null;
      this._ngZone.run(() => this._router.navigate(['login']).then());
    });
  }

  private _finish() {
    if (this._count > 10) {
      this._router.navigate(['the-secret']).then();
    } else {
      this._count = 0;
    }
  }
}
