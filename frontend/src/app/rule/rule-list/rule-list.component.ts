import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatCheckbox } from '@angular/material/checkbox';

interface Rule {
  id: number;
  name: string;
}

@Component({
  selector: 'app-rule-list',
  templateUrl: './rule-list.component.html',
  styleUrls: ['./rule-list.component.css']
})
export class RuleListComponent {
  rules: Rule[] = [
    { id: 1, name: 'Правило 1 теоретически будет длинное' },
    { id: 2, name: 'Правило 2' },
    { id: 3, name: 'Правило 3' },
    { id: 4, name: 'Правило 4' },
    { id: 5, name: 'Правило 5' },
    { id: 6, name: 'Правило 6' },
  ];

  @Input() selectedRules: any[] = [];
  @Output() result = new EventEmitter<number[]>();
  @Output() selectForAll = new EventEmitter<number[]>();

  checkSelection(item: number): boolean {
    return this.selectedRules.includes(item);
  }

  toggleSelection(item: number, checkbox: MatCheckbox): void {
    if (checkbox.checked) {
      this.selectedRules.push(item);
    } else {
      this.selectedRules.splice(this.selectedRules.indexOf(item), 1);
    }
    this.filterChange();
  }

  filterChange() {
    console.log(this.selectedRules)
    this.result.emit(this.selectedRules);
  }

  selectAll() {
    if(this.selectedRules.length == this.rules.length) {
      this.selectedRules = [];
    } else {
      this.selectedRules = this.rules.map(rule => rule.id);
    }
    this.filterChange()
  }

  selectForAllSessions() {
    this.selectForAll.emit(this.selectedRules);
  }
}
