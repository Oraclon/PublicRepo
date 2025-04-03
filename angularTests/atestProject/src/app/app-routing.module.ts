import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DemohomeComponent } from './pages/demohome/demohome.component';
import { SignalsComponent } from './pages/signals/signals.component';
import { FormComponent } from './pages/form/form.component';

const routes: Routes = [
  {path:"", redirectTo: "/home", pathMatch: "full"},
  {path:"home", component: DemohomeComponent},
  {path:"signals", component: SignalsComponent},
  {path:"form", component: FormComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
