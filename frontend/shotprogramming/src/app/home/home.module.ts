import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DeployEditionComponent } from './deploy-edition/deploy-edition.component';
import {
  MatButtonModule,
  MatCardModule,
  MatFormFieldModule, MatGridListModule,
  MatIconModule,
  MatInputModule, MatProgressSpinnerModule,
  MatSnackBarModule
} from "@angular/material";
import { HomeComponent } from './home/home.component';
import {RouterModule} from "@angular/router";

@NgModule({
  declarations: [DeployEditionComponent, HomeComponent],
  imports: [
    CommonModule,
    RouterModule,
    MatButtonModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    MatGridListModule
  ]
})
export class HomeModule { }
