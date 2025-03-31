export interface iSelection
{
    id: number | null;
    value: string;
    description: string | null;
    selected: boolean;
}

export class SelectionItem implements iSelection
{
    id!: number | null;
    value!: string;
    description!: string | null;
    selected: boolean = false;

    constructor(public item:iSelection)
    {
        Object.assign(this, item);
    }

    changeStatus():void
    {
        this.selected = !this.selected;
    }
} 

export class SelectionItemsBlock
{
    data: SelectionItem[] = [];

    constructor(data: iSelection[])
    {
        let generated: SelectionItem[] = [];
        for(let x: number = 0; x < data.length; x++)
            generated.push(new SelectionItem(data[x]));
        this.data = generated;
    }

    clearSelections():void
    {
        this.data.map((x:SelectionItem)=> {x.selected = false; return x;})
    }

    set value (value: string | null)
    {
        if(value != null)
        {
            let container = value.split("-");
            for(let x: number = 0; x < this.data.length; x++)
                if(container.includes(this.data[x].value))
                    this.data[x].selected = true;            
        }
    }
    get value(): string | null
    {
        let selection: SelectionItem[] = this.data.filter((x:SelectionItem)=> x.selected);
        return selection.length > 0 ? selection.map((x:SelectionItem)=> x.value).join(",") : null;
    }
}