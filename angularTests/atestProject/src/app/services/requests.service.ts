import { HttpClient } from "@angular/common/http";
import { TestPostClass } from "../interfaces/interfaces";
import { Observable, of } from "rxjs";
import { Injectable } from "@angular/core";

@Injectable()
export class ReqService
{
    constructor(private http: HttpClient){}
    private _objservables: Observable<any>[]= [];
    controllers = {
        demo: "https://my-json-server.typicode.com/JSGund/XHR-Fetch-Request-JavaScript/posts"
    }
    
    getDemoData():Observable<TestPostClass[]>
    {
        let obs = this.http.get<TestPostClass[]>(this.controllers.demo, {});
        this._objservables.push(obs);
        return obs;
    }
    clearAllObs():void
    {
    }
}