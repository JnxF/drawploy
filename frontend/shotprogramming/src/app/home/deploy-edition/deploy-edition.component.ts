import {Component, HostBinding, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {MatInput, MatSnackBar} from "@angular/material";
import {ApiService} from "../../api/api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {ErrorToStringService} from "../../api/error-to-string.service";
import {Deployment} from "../../model/deployment";

@Component({
  selector: 'app-deploy-edition',
  templateUrl: './deploy-edition.component.html',
  styleUrls: ['./deploy-edition.component.scss']
})
export class DeployEditionComponent implements OnInit, OnDestroy {
  public deployment: Deployment = null;
  public loading = false;
  public deployed = false;

  private _closed = false;

  @ViewChild(MatInput) private _input: MatInput;

  constructor(private _matSnackbar: MatSnackBar, private _api: ApiService, private _error: ErrorToStringService,
              private _router: Router) {
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
        this.loading = true;
        this._api.post('page/', {
          image: base64
        }).subscribe((obj: any) => {
            this.deployment = {
              id: obj.content.targetId,
              nameOperation: obj.content.name,
              code: obj.content.code
            };
            this.deployed = true;
            this._reloadDeploy();
          },
          err => this._displayError(this._error.errorToString(err)));
      });
    } else {
      this._displayError('Only images allowed.');
    }
  }

  private _reloadDeploy() {
    this._api.get<any>(
      `page/${this.deployment.id}/status/`, undefined,
      {operationName: this.deployment.nameOperation}
    ).subscribe(deployment => {
      if (deployment.content.status === 'DONE') {
        this._router.navigate(['home']).then();
      }
    });
    if (!this._closed) {
      setTimeout(() => this._reloadDeploy(), 3000);
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

  ngOnDestroy(): void {
    this._closed = true;
  }

  ngOnInit(): void {
  }

  private _displayError(error: string) {
    this._matSnackbar.open(error, 'Ok', {duration: 3000})
  }
}
