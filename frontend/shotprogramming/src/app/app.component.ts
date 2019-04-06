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
  constructor(public api: ApiService,
              private _router: Router,
              private _ngZone: NgZone) {
  }

  public signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(() => {
      this.api.googleUser = null;
      this._ngZone.run(() => this._router.navigate(['login']).then());
    });
  }
}
