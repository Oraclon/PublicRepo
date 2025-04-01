import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AcomponentComponent } from './acomponent/acomponent.component';
import { SignalButtonComponent } from './signalSendRead/signal-button/signal-button.component';
import { SignalReadComponent } from './signalSendRead/signal-read/signal-read.component';
import { MainService } from './services/mainService.service';
import { SignalObjComponent } from './signalObj/signal-obj/signal-obj.component';
import { ReceiveObjComponent } from './signalObj/receive-obj/receive-obj.component';
import { SendSarrayComponent } from './signalArr/send-sarray/send-sarray.component';
import { ReceiveSarrayComponent } from './signalArr/receive-sarray/receive-sarray.component';
import { ViewUpdateComponent } from './signalView/view-update/view-update.component';
import { ViewControlComponent } from './signalView/view-control/view-control.component';

@NgModule({
  declarations: [
    AppComponent,
    AcomponentComponent,
    SignalButtonComponent,
    SignalReadComponent,
    SignalObjComponent,
    ReceiveObjComponent,
    SendSarrayComponent,
    ReceiveSarrayComponent,
    ViewUpdateComponent,
    ViewControlComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [MainService],
  bootstrap: [AppComponent]
})
export class AppModule { }
