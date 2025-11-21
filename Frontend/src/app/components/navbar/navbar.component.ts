import { Component, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  isScrolled = false;
  private lastScrollY = window.scrollY;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    const currentScrollY = window.scrollY;
    if (currentScrollY > 50 && currentScrollY > this.lastScrollY) {
      // Scrolling down, contract navbar
      this.isScrolled = true;
    } else if (currentScrollY < this.lastScrollY) {
      // Scrolling up, expand navbar
      this.isScrolled = false;
    } else if (currentScrollY <= 50) {
      // Near top, always expanded
      this.isScrolled = false;
    }
    this.lastScrollY = currentScrollY;
  }

  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
