import { Injectable, OnInit, signal } from "@angular/core";
import { iTestInterface, TestPost, TestPostClass, TestUser } from "../interfaces/interfaces";
import { ViewType } from "../signalView/view-update/view-update.component";

@Injectable()
export class MainService
{
    public sig = signal<number>(0);
    public testSignal = signal<iTestInterface>( { id:0, value: null } )
    private test: string[] = ["a","B"]
    public arraySignal = signal<string[]>([]);
    public viewSignal = signal<ViewType>(ViewType.None);
    public httpSignal = signal<TestPostClass[]>([]);
    public intervalSignal = signal<number>(0);
    public loginSignal = signal<boolean>(false);

    interval = setInterval(()=>{
        this.arraySignal.set(this.test);
        clearInterval(this.interval);
    }, 2000)
}