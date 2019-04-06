import {Component, OnInit} from '@angular/core';
import {MatSnackBar} from "@angular/material";
import {ApiService} from "../../api/api.service";
import {ActivatedRoute} from "@angular/router";
import {ErrorToStringService} from "../../api/error-to-string.service";
import {Deployment} from "../../model/deployment";

@Component({
  selector: 'app-home',
  templateUrl: './deploy-edition.component.html',
  styleUrls: ['./deploy-edition.component.scss']
})
export class DeployEditionComponent {
  public deployment: Deployment = null;

  public get deploymentStr(): string {
    return JSON.stringify(this.deployment, null, 2);
  }

  constructor(private _matSnackbar: MatSnackBar, private _api: ApiService, private _error: ErrorToStringService,
              private _route: ActivatedRoute) {
    if (this._route.snapshot.fragment) {
      // TODO: get the deployment with id this._route.snapshot.fragment into deployment
    }
  }

  public onFileChange(event) {
    const files: FileList = event.target.files;
    if (files.length > 1) {
      this._displayError('Only one file per time allowed.');
      return;
    }
    const picture = files.item(0);
    if (picture.type.startsWith('image/')) {
      this._fileTo64Base(picture).then(base64 => {
        this._api.post('page/', {
          image: base64
        }).subscribe((obj: any) => this.deployment = obj.content,
            err => this._displayError(this._error.errorToString(err)));
      });
    } else {
      this._displayError('Only images allowed.');
    }
  }

  private _fileTo64Base(file: File): Promise<string> {
    return new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      // Closure to capture the file information.
      reader.onloadend = (e: any) => {
        let str = e.target.result;
        const commaIdx = str.indexOf(',');
        if (commaIdx >= 0) {
          str = str.substring(commaIdx+1);
        }
        resolve(str);
      };
      reader.readAsDataURL(file);
    });
  }

  private _displayError(error: string) {
    this._matSnackbar.open(error, 'Ok', {duration: 3000})
  }
}
