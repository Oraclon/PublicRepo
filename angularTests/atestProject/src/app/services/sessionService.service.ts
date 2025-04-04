import { computed, Injectable, Signal } from "@angular/core";
import { MainService } from "./mainService.service";
import { Router } from "@angular/router";
export interface SessionInt
{
    sessionId: string;
    user: string; 
    mail: string;
}
@Injectable()
export class SessionService{
    constructor(private ms: MainService, private router: Router){}
    private _sessionName: string = "bel";
    private _logged: Signal<boolean> = computed(()=>{ return this.ms.loginSignal(); });

    checkLogin(): boolean
    {
        let loginStatus: boolean = localStorage.getItem(this._sessionName) != null; 
        this.ms.loginSignal.set(loginStatus);
        return loginStatus;
    }
    login():void
    {
        let obj = { sessionId: "daslkjdlasdlask", user: "bel@oraclon.gr", mail: "info@oraclon.gr" }
        localStorage.setItem(this._sessionName, JSON.stringify(obj));
        this.ms.loginSignal.set(true);
    }
    logout():void
    {
        localStorage.removeItem(this._sessionName);
        this.ms.loginSignal.set(false);
        this.router.navigate(["/signals"]);
    }
    autoLoginLogoutAction():void
    {
        this._logged() ? this.logout() : this.login();
    }
}