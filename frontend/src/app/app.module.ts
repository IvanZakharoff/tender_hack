import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MaterialModule } from './modules/materials.module';
import { QuotationSessionsComponent } from './quotation-sessions/quotation-sessions.component';
import { RuleListComponent } from './rule/rule-list/rule-list.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FileUploadService } from './upload-service';
import { HttpClientModule } from '@angular/common/http';
import { CheckingResultComponent } from './checking-result/checking-result.component';
import { SuccessPageComponent } from './success-page/success-page.component';

@NgModule({
  declarations: [
    AppComponent,
    QuotationSessionsComponent,
    RuleListComponent,
    CheckingResultComponent,
    SuccessPageComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [
    provideAnimationsAsync(),
    FileUploadService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
