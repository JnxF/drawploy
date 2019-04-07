import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {DeployEditionComponent} from "./home/deploy-edition/deploy-edition.component";
import {LoginComponent} from "./login/login.component";
import {HomeComponent} from "./home/home/home.component";
import {SessionGuard} from "./api/session.guard";
import {TheSecretComponent} from "./home/the-secret/the-secret.component";
import {MaquinasComponent} from "./home/maquinas/maquinas.component";

const routes: Routes = [
  {
    path: 'deploy-edition',
    component: DeployEditionComponent,
    canActivate: [SessionGuard]
  },
  {
    path: 'the-secret',
    component: TheSecretComponent,
    canActivate: [SessionGuard]
  },
  {
    path: 'home',
    component: HomeComponent,
    canActivate: [SessionGuard]
  },
  {
    path: 'maquinas',
    component: MaquinasComponent,
    canActivate: [SessionGuard]
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: 'home'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
