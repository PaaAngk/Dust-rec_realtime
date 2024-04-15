import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, Input, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { TuiComparator, TuiTableModule } from '@taiga-ui/addon-table';
import { TuiDay, TuiDayRange, tuiToInt } from '@taiga-ui/cdk';
import { TuiButtonModule, TuiLoaderModule, TuiScrollbarModule } from '@taiga-ui/core/components';
import {TuiCalendarRangeModule, TuiInputDateRangeModule, tuiCreateDefaultDayRangePeriods} from '@taiga-ui/kit';
import { TableService } from './table.service';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';

interface User {
    readonly dob: TuiDay;
    readonly name: string;
}
 
const TODAY = TuiDay.currentLocal();
const FIRST = [
    'John',
    'Jane',
    'Jack',
    'Jill',
    'James',
    'Joan',
    'Jim',
    'Julia',
    'Joe',
    'Julia',
];
 
const LAST = [
    'Smith',
    'West',
    'Brown',
    'Jones',
    'Davis',
    'Miller',
    'Johnson',
    'Jackson',
    'Williams',
    'Wilson',
];
 
const DATA: readonly User[] = Array.from({length: 300}, () => ({
    name: `${LAST[Math.floor(Math.random() * 10)]}, ${
        FIRST[Math.floor(Math.random() * 10)]
    }`,
    dob: TODAY.append({day: -Math.floor(Math.random() * 4000) - 7500}),
}));
 
function getAge({dob}: User): number {
    const years = TODAY.year - dob.year;
    const months = TODAY.month - dob.month;
    const days = TODAY.day - dob.day;
    const offset = tuiToInt(months > 0 || (!months && days > 9));
 
    return years + offset;
}

const today = TuiDay.currentLocal();
const yesterday = today.append({day: -1});

interface HistoryData{
    dateFrom: Date,
    dateTo: Date,
    duration: number,
}

@Component({
	standalone: true,
	selector: 'app-table',
	templateUrl: './table.component.html',
	styleUrls: ['./table.component.less'],
	imports: [
		CommonModule,
        FormsModule,
        ReactiveFormsModule,

		TuiLoaderModule,
		TuiInputDateRangeModule,
		TuiButtonModule,
		TuiTableModule,
		TuiScrollbarModule,
	],
	// changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TableComponent {
    readonly control = new FormControl(new TuiDayRange(yesterday, today));
    tableData:HistoryData[] = [] as HistoryData[];

	readonly data = DATA;
	readonly columns = ['dateFrom', 'dateTo', 'duration'];
 
	loading = false;
	@Input() videoLink = "http://localhost:888/stream/index.m3u8";

	items = tuiCreateDefaultDayRangePeriods(['За все время ', 'Сегодня', 'Вчера', 'Текущая неделя', 'Текущий месяц', 'Предыдущий месяц']);
	// ['За все время', 'Сегодня', 'Вчера', 'Текущая неделя', 'Текущий месяц', 'Предыдущий месяц'] 
    
	constructor(
        private tableService: TableService
	) {}

	ngOnInit() {
        this.tableService.history_data
        .subscribe({
            next:(data:any) => {
                this.tableData = data; 
            }
        });
	}

    search_click(){
        this.tableService.get_history_data('city-traffic', 1710161738277, 1710164143441)
        console.log("Click")
    }
    

}
