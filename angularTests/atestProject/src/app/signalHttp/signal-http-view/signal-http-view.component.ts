import { Component, computed, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';

@Component({
  selector: 'app-signal-http-view',
  standalone: false,
  templateUrl: './signal-http-view.component.html',
  styleUrl: './signal-http-view.component.scss'
})
export class SignalHttpViewComponent {
  constructor(private ms: MainService){}

  totals:Signal<number> = computed(()=>{ return this.ms.httpSignal().length; })
}
