import { animate, state, style, transition, trigger } from '@angular/animations';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

interface Rule {
  id: string;
  passed: boolean;
  reason: string | null;
  showReason: boolean;
}

interface Session {
  name: string;
  rules: Rule[];
}

@Component({
  selector: 'app-checking-result',
  templateUrl: './checking-result.component.html',
  styleUrl: './checking-result.component.css',
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0', visibility: 'hidden'})),
      state('expanded', style({height: 'auto', visibility: 'visible'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
  ])
  ],
})
export class CheckingResultComponent implements OnInit {

  rules = [
    { id: 1, name: 'Правило 1 теоретически будет длинное' },
    { id: 2, name: 'Правило 2' },
    { id: 3, name: 'Правило 3' },
    { id: 4, name: 'Правило 4' },
    { id: 5, name: 'Правило 5' },
    { id: 6, name: 'Правило 6' },
  ];


  sessions: any[] = [];
  displayedColumns: string[] = ['expand', 'rule', 'status'];
  expandedElement: { sessionName: string; ruleId: number } | null = null;


  constructor(private router: Router) { }

  ngOnInit() {
    const sessionsData = [
      {
        name: 'Session 1',
        rules: [
          {
            id: 1,
            passed: true,
            reason: 'Описание: Все необходимые поля заполнены корректно.',
          },
          {
            id: 3,
            passed: false,
            reason: 'Ошибка: Превышен лимит количества символов в названии.',
          },
          {
            id: 4,
            passed: true,
            reason: null, // Нет описания для пройденного правила
          },
        ],
      },
      {
        name: 'Session 2',
        rules: [
          {
            id: 2,
            passed: false,
            reasonv: 'Ошибка: Не пройдена проверка на уникальность.',
          },
          {
            id: 5,
            passed: true,
            reason: null,
          },
          {
            id: 6,
            passed: false,
            reason: 'Ошибка: Неправильный формат данных.',
          },
        ],
      },
    ];
    this.sessions = history.state.data;
    this.sessions = sessionsData;

  }

  toggleReason(rule: Rule) {
    rule.showReason = !rule.showReason
  }

  toggleExpandedElement(sessionName: string, ruleId: number) {
    if (this.expandedElement && this.expandedElement.sessionName === sessionName && this.expandedElement.ruleId === ruleId) {
      this.expandedElement = null;
    } else {
      this.expandedElement = { sessionName, ruleId };
    }
  }

  isExpanded(sessionName: string, ruleId: number): boolean {
    return this.expandedElement?.sessionName === sessionName && this.expandedElement?.ruleId === ruleId;
  }

  isDetailRow = (index: number, row: any) => row.hasOwnProperty('reason');

  delete() {
    this.router.navigate(['/success']);
  }

  findRuleById(id: number) {
    return this.rules.find(rule => rule.id = id)?.name
  }

}
