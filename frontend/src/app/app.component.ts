import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="app-container">
      <header>
        <nav>
          <div class="logo">
            <h1>DataMAx</h1>
            <p>Pharmaceutical Data Analytics Platform</p>
          </div>
          <ul class="nav-links">
            <li><a routerLink="/dashboard" routerLinkActive="active">Dashboard</a></li>
            <li><a routerLink="/drugs" routerLinkActive="active">Drugs</a></li>
            <li><a routerLink="/trials" routerLinkActive="active">Clinical Trials</a></li>
          </ul>
        </nav>
      </header>
      
      <main>
        <router-outlet></router-outlet>
      </main>
      
      <footer>
        <p>&copy; 2024 DataMAx Platform | Associate Software Engineer Portfolio Project</p>
      </footer>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: #2c3e50;
      color: white;
      padding: 0 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    nav {
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 15px 0;
    }

    .logo h1 {
      margin: 0;
      font-size: 28px;
      color: #3498db;
    }

    .logo p {
      margin: 5px 0 0 0;
      font-size: 12px;
      color: #bdc3c7;
    }

    .nav-links {
      list-style: none;
      display: flex;
      gap: 30px;
      margin: 0;
      padding: 0;
    }

    .nav-links a {
      color: white;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 4px;
      transition: background 0.3s;
    }

    .nav-links a:hover {
      background: #34495e;
    }

    .nav-links a.active {
      background: #3498db;
    }

    main {
      flex: 1;
      background: #ecf0f1;
      padding: 20px 0;
    }

    footer {
      background: #2c3e50;
      color: #bdc3c7;
      text-align: center;
      padding: 20px;
      margin-top: auto;
    }

    footer p {
      margin: 0;
      font-size: 14px;
    }
  `]
})
export class AppComponent {
  title = 'DataMAx';
}
