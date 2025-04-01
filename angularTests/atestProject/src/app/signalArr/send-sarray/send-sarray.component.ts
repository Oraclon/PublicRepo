import { Component, computed, Renderer2, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';

@Component({
  selector: 'app-send-sarray',
  standalone: false,
  templateUrl: './send-sarray.component.html',
  styleUrl: './send-sarray.component.scss'
})
export class SendSarrayComponent {
  constructor(private ms: MainService, private rend: Renderer2){}

  arraySize: Signal<number> = computed(()=>{ return this.ms.arraySignal().length })
  inputValue: string = "";

  updateInputValue(input: HTMLInputElement)
  {
    let int = setInterval(()=>{
    console.log(input)
      this.inputValue = input.value;
      clearInterval(int)
    },40)
  }
  sendToArray(input: HTMLInputElement):void
  {
    if(input.value != "")
    {
      this.rend.setProperty(input, "value",null);
      this.ms.arraySignal.update((values:string[])=> ([...values, this.inputValue]))
    }
  }
  clearArray():void
  {
    this.ms.arraySignal.set([])
  }
}
