import { Component, computed, OnInit, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';
import { SessionService } from '../../services/sessionService.service';

@Component({
  selector: 'app-signals',
  standalone: false,
  templateUrl: './signals.component.html',
  styleUrl: './signals.component.scss'
})
export class SignalsComponent implements OnInit{
  constructor(private ss: SessionService, private ms: MainService){}

  loggedIn: Signal<boolean> = computed(()=> { return this.ms.loginSignal(); })

  ngOnInit(): void {
    this.ss.checkLogin();
  }

  logged: Signal<boolean> = computed(()=>{ return this.ms.loginSignal(); });

  login():void{ this.ss.login() }
  logout():void{ this.ss.logout() }
}
