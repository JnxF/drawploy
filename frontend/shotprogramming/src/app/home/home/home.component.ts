import {Component, OnInit} from '@angular/core';
import {MatSnackBar} from "@angular/material";
import {ApiService} from "../../api/api.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.sass']
})
export class HomeComponent implements OnInit {

  constructor(private _matSnackbar: MatSnackBar, private _api: ApiService) {
  }

  ngOnInit() {
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
        this._api.post('page', {
          image: base64
        }).subscribe(obj => console.log(obj));
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
        resolve(e.target.result);
      };
      reader.readAsDataURL(file);
    });
  }

  private _displayError(error: string) {
    this._matSnackbar.open(error, 'Ok', {duration: 3000})
  }
}
