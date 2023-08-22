import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';


import { LandingComponent } from './landing/landing.component';
import { ChatComponent } from './chat/chat.component';
import {CsComponent} from "./cs/cs.component";
const routes: Routes = [
  { path: 'chat', component: ChatComponent },
  { path: 'cs', component: CsComponent },
  { path: '', component: LandingComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
