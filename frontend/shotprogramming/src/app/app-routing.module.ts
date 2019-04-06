import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {DeployEditionComponent} from "./home/deploy-edition/deploy-edition.component";
import {LoginComponent} from "./login/login.component";
import {HomeComponent} from "./home/home/home.component";
import {SessionGuard} from "./api/session.guard";

const routes: Routes = [
  {
    path: 'deploy-edition',
    component: DeployEditionComponent,
    canActivate: [SessionGuard]
  },
  {
    path: 'home',
    component: HomeComponent,
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
