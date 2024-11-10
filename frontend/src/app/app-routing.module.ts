import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { QuotationSessionsComponent } from './quotation-sessions/quotation-sessions.component';
import { CheckingResultComponent } from './checking-result/checking-result.component';

const routes: Routes = [
  { path: 'sessions', component: QuotationSessionsComponent },
  { path: 'checking-result', component: CheckingResultComponent },
  { path: '', redirectTo: '/sessions', pathMatch: 'full' }, // Редирект на основной путь
  { path: '**', redirectTo: '/sessions' }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
