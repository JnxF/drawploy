import {Component} from '@angular/core';
import {ApiService} from "../../api/api.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-maquinas',
  templateUrl: './maquinas.component.html',
  styleUrls: ['./maquinas.component.scss']
})
export class MaquinasComponent {
  public maquinas = [];

  constructor(private _api: ApiService, route: ActivatedRoute) {
    this._api.get<any>(`page/${route.snapshot.queryParams.id}/metrics/`, undefined,
      {region: route.snapshot.queryParams.region})
      .subscribe(response => this.maquinas = response.content.items);
  }
}
