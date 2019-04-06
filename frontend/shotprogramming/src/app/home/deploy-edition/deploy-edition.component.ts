import {Component, ViewChild} from '@angular/core';
import {MatInput, MatSnackBar} from "@angular/material";
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
  public loading = false;
  public editedDeploy = false;

  @ViewChild(MatInput) private _input: MatInput;

  public get deploymentStr(): string {
    return JSON.stringify(this.deployment.code, null, 2);
  }

  constructor(private _matSnackbar: MatSnackBar, private _api: ApiService, private _error: ErrorToStringService,
              private _route: ActivatedRoute) {
    if (this._route.snapshot.fragment) {
      this.loading = true;
      this._api.get<any>(
        `page/${this._route.snapshot.fragment}`
      ).subscribe(deployment => {
        this.deployment = {id: deployment.content.id, code: deployment.content.code};
        this.editedDeploy = false;
        this.loading = false;
      }, err => this._displayError(this._error.errorToString(err)));
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
        }).subscribe((obj: any) => {
            this.deployment = {id: obj.content.targetId, code: obj.content.code};
            this.editedDeploy = false;
          },
          err => this._displayError(this._error.errorToString(err)));
      });
    } else {
      this._displayError('Only images allowed.');
    }
  }

  public deploy() {
    if (this._input && this.deployment) {
      this._api.post(`page/${this.deployment.id}/deploy`, {})
        .subscribe(() => {
          this._matSnackbar.open('Deployed!', 'Ok', {duration: 5000});
        }, err => this._displayError(this._error.errorToString(err)));
    }
  }

  public save() {
    if (this._input && this.deployment) {
      const newDeploy = JSON.parse(this._input.value);
      this._api.post(`page/${this.deployment.id}`, {content: newDeploy})
        .subscribe((obj: any) => {
          this.deployment = obj.content;
          this.editedDeploy = false;
        });
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
          str = str.substring(commaIdx + 1);
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
