import { Component, computed, signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';

@Component({
  selector: 'app-signal-button',
  standalone: false,
  templateUrl: './signal-button.component.html',
  styleUrl: './signal-button.component.scss'
})
export class SignalButtonComponent {
  constructor(private ms: MainService){}

  increase():void
  {
    this.ms.sig.update(x=> x+1);
  }
  decrease():void
  {
    this.ms.sig.update(x=> x>0 ? x-1 : 0);
  }
  reset():void
  {
    this.ms.sig.set(0);
  }
}
