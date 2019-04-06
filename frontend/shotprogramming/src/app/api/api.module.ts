import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from "@angular/common/http";
import {ApiService} from "./api.service";

@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ],
  providers: [ApiService]
})
export class ApiModule { }
