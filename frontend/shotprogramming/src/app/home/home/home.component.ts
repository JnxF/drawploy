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

  edit(deploymentId: string) {
    this._router.navigate(['deploy-edition'], {fragment: deploymentId}).then();
  }

  ngOnInit() {
    // TODO: ask for deployments and save in deployments
    this.deployments.push({
      name: 'quickstart-deployment',
      id: '54660732508021769'
    });
  }

}
