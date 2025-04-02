import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DemohomeComponent } from './pages/demohome/demohome.component';
import { SignalsComponent } from './pages/signals/signals.component';

const routes: Routes = [
  {path:"", redirectTo: "/home", pathMatch: "full"},
  {path:"home", component: DemohomeComponent},
  {path:"signals", component: SignalsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
