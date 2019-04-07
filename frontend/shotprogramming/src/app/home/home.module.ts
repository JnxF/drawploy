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
import { TheSecretComponent } from './the-secret/the-secret.component';
import { MaquinasComponent } from './maquinas/maquinas.component';

@NgModule({
  declarations: [DeployEditionComponent, HomeComponent, TheSecretComponent, MaquinasComponent],
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
