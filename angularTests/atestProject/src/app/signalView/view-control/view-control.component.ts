import { Component } from '@angular/core';
import { ViewType } from '../view-update/view-update.component';
import { MainService } from '../../services/mainService.service';

@Component({
  selector: 'app-view-control',
  standalone: false,
  templateUrl: './view-control.component.html',
  styleUrl: './view-control.component.scss'
})
export class ViewControlComponent {
  constructor(private ms: MainService){}
  viewType: typeof ViewType = ViewType;

  setView(view: ViewType)
  {
    this.ms.viewSignal.set(view);
  }
}
