import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';

@Injectable({
	providedIn: 'root',
})
export class TableService {
	private historyData = new BehaviorSubject<any>({});

	constructor(private http: HttpClient){}

	get history_data(){
		return this.historyData.asObservable()
	}

	get_history_data(source: string, from: Date | number, to: Date | number){
		//   1710161738277     1710164143441
		this.http.get(`http://localhost:8500/history?source=${source}&timestamp_from=${from}&timestamp_to=${to}`, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
              }        
        }).subscribe({
			next:(data:any) => {
				this.historyData.next(data); 
				console.log(data)
			}
		});
        
	}

}
