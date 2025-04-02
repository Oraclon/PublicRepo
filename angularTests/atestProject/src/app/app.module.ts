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
import { SignalHttpComponent } from './signalHttp/signal-http/signal-http.component';
import { SignalHttpViewComponent } from './signalHttp/signal-http-view/signal-http-view.component';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MainMenuComponent } from './plugins/main-menu/main-menu.component';
import { DemohomeComponent } from './pages/demohome/demohome.component';
import { SignalsComponent } from './pages/signals/signals.component';

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
    ViewControlComponent,
    SignalHttpComponent,
    SignalHttpViewComponent,
    MainMenuComponent,
    DemohomeComponent,
    SignalsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [MainService],
  bootstrap: [AppComponent]
})
export class AppModule { }
