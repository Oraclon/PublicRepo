import { Component, computed, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';
import { SessionService } from '../../services/sessionService.service';

@Component({
  selector: 'app-main-menu',
  standalone: false,
  templateUrl: './main-menu.component.html',
  styleUrl: './main-menu.component.scss'
})
export class MainMenuComponent {
  constructor(private ms: MainService, private ss: SessionService){}
  logged: Signal<boolean> = computed(()=>{
    return this.ms.loginSignal();
  });
  loginLogoutAction():void
  {
    this.ss.autoLoginLogoutAction();
  }
}
