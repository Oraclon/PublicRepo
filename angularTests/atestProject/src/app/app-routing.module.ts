import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DemohomeComponent } from './pages/demohome/demohome.component';
import { SignalsComponent } from './pages/signals/signals.component';
import { FormComponent } from './pages/form/form.component';
import { LoggedInComponent } from './logged-in/logged-in.component';
import { authGuardGuard } from './auth-guard.guard';
import { productResolver } from './resolveData.guard';

const routes: Routes = [
  {path:"", redirectTo: "/home", pathMatch: "full"},
  {path:"home", component: DemohomeComponent},
  {path:"signals", component: SignalsComponent},
  {path:"form", component: FormComponent},
  {path:"bel", component: LoggedInComponent, resolve:[productResolver], canActivate:[authGuardGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
