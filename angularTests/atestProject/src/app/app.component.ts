import { Component, OnInit } from '@angular/core';
import { iSelection, SelectionItem, SelectionItemsBlock } from './common/interfaces';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  title = 'atestProject';
  items: iSelection[] = [...Array(20).keys()].map((x:number)=> ({id: x, value: x.toString(), description:`desc-${x}` } as iSelection));
  selectionsBlock: SelectionItemsBlock = new SelectionItemsBlock(this.items);

  ngOnInit(): void {
    this.selectionsBlock.value = "0-3-4-6-12";
  }

  private _updateValue():void
  {
    console.log(this.selectionsBlock.value);
  }

  changeSelection(item:SelectionItem):void
  {
    item.changeStatus();
    this._updateValue();
  }
  clearSelections():void
  {
    this.selectionsBlock.clearSelections();
    this._updateValue();
  }
}
