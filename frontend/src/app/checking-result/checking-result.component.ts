import { animate, state, style, transition, trigger } from '@angular/animations';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

interface Rule {
  id: string;
  status: string;
  reason: string | null;
}

interface Session {
  name: string;
  url: string;
  rules: Rule[];
}

@Component({
  selector: 'app-checking-result',
  templateUrl: './checking-result.component.html',
  styleUrl: './checking-result.component.css',
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

  statuses = [
    { systemName: 'succeed', name: 'Пройдено' },
    { systemName: 'unsucceed', name: 'Не пройдено' },
    { systemName: 'warning', name: 'Неопределен' },
  ]

  sessions: any[] = [];
  displayedColumns: string[] = ['expand', 'rule', 'status'];
  expandedElement: { sessionName: string; ruleId: number } | null = null;
  expandedRule: number | null = null;

  constructor(private router: Router) { }

  ngOnInit() {
    const sessionsData = [
      {
        name: 'Session 1',
        url: 'lll',
        rules: [
          {
            id: 1,
            status: 'succeed',
            reason: 'Описание: Все необходимые поля заполнены корректно.',
          },
          {
            id: 3,
            status: 'succeed',
            reason: 'Ошибка: Превышен лимит количества символов в названии.',
          },
          {
            id: 4,
            status: 'succeed',
            reason: null, // Нет описания для пройденного правила
          },
        ],
      },
      {
        name: 'Session 2',
        url: 'lll',
        rules: [
          {
            id: 2,
            status: 'warning',
            reasonv: 'Ошибка: Не пройдена проверка на уникальность.',
          },
          {
            id: 5,
            status: 'succeed',
            reason: null,
          },
          {
            id: 6,
            status: 'unsucceed',
            reason: 'Ошибка: Неправильный формат данных.',
          },
        ],
      },
    ];
    this.sessions = history.state.data;
    this.sessions = sessionsData;

  }

  delete() {
    this.router.navigate(['/success']);
  }

  findRuleById(id: number) {
    return this.rules.find(rule => rule.id == id)?.name
  }

  findStatusBySystemName(systemName: string) {
    return this.statuses.find(status => status.systemName == systemName)?.name
  }

  setExpandedRule(ruleId: number | null): void {
    this.expandedRule = ruleId;
  }

  checkSelection(session: Session) {
    return session.rules.some(rule => rule.status != 'succeed');
  }
}
