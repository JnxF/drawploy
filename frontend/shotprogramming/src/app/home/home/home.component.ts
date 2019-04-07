import {Component, OnInit} from '@angular/core';
import {DeploymentShort} from "../../model/deployment";
import {ApiService} from "../../api/api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  public deployments: DeploymentShort[] = [];

  constructor(private _api: ApiService, private _router: Router) {
  }

  edit(id: string, region: string) {
    this._router.navigate(['maquinas'], {queryParams: {id: id, region: region}});
  }

  ngOnInit() {
    this._api.get<{ content: any }>('page/').subscribe((response: { content: DeploymentShort[] }) => {
      if (response.content) {
        this.deployments = response.content;
      }
    });
  }

}
