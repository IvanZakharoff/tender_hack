import { Component, OnInit } from '@angular/core';

interface Rule {
  id: string;
  passed: boolean;
  reason: string | null;
  showReason?: boolean;
}

interface Session {
  sessionName: string;
  rules: Rule[];
}

@Component({
  selector: 'app-checking-result',
  templateUrl: './checking-result.component.html',
  styleUrl: './checking-result.component.css'
})
export class CheckingResultComponent implements OnInit {
  sessions: any[] = [];
  displayedColumns: string[] = ['rule', 'status'];


  constructor() { }

  ngOnInit() {
    const sessionsData = [
      {
        sessionName: 'Session 1',
        rules: [
          {
            id: 'rule1',
            passed: true,
            description: 'Описание: Все необходимые поля заполнены корректно.',
          },
          {
            id: 'rule2',
            passed: false,
            description: 'Ошибка: Превышен лимит количества символов в названии.',
          },
          {
            id: 'rule3',
            passed: true,
            description: null, // Нет описания для пройденного правила
          },
        ],
      },
      {
        sessionName: 'Session 2',
        rules: [
          {
            id: 'rule1',
            passed: false,
            description: 'Ошибка: Не пройдена проверка на уникальность.',
          },
          {
            id: 'rule2',
            passed: true,
            description: null,
          },
          {
            id: 'rule3',
            passed: false,
            description: 'Ошибка: Неправильный формат данных.',
          },
        ],
      },
    ];
    this.sessions = history.state.data;
    this.sessions = sessionsData;
    
  }

  toggleReason(rule: Rule) {
    rule.showReason = !rule.showReason;
  }

}
