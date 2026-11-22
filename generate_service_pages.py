# -*- coding: utf-8 -*-
"""
RVRR Construction & Property Sales
Generates an individual HTML page for every sub-service, using one shared
template so the header, footer and styling stay identical across all pages.

Run:  python generate_service_pages.py
"""
import os
import json

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Live domain — replace before publishing.
BASE = "https://www.rvrrconstruction.in"

# ---- Category-level metadata (badge icon + anchor on services.html) ----
CATEGORIES = {
    "construction": {
        "name": "Construction",
        "anchor": "services.html#construction",
        "kw": "construction company, building contractors, civil construction, building construction services",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 20h20"/><path d="M4 20V8l8-5 8 5v12"/><path d="M9 20v-6h6v6"/></svg>',
    },
    "interior": {
        "name": "Interior Design",
        "anchor": "services.html#interior",
        "kw": "interior design, interior designers, modular interiors, turnkey interiors",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>',
    },
    "property": {
        "name": "Property Sales",
        "anchor": "services.html#property",
        "kw": "property for sale, real estate, buy property, property dealers, real estate agents",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg>',
    },
}

CHECK = "check"  # marker for check-list icon

# ---- Every sub-service ----
# slug, category, name, hero image, intro (banner sub / lead), two overview paras,
# highlights (check-list), offer cards [(title, text)]
SERVICES = [
    # ---------------- CONSTRUCTION ----------------
    {
        "slug": "commercial-project-construction", "cat": "construction",
        "name": "Commercial Project Construction",
        "img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=80",
        "intro": "Commercial-grade buildings engineered for business, built to last and delivered on schedule.",
        "p1": "From retail complexes and showrooms to offices and mixed-use developments, RVRR delivers commercial construction that meets the highest standards of strength, safety and finish. We understand that a commercial project is an investment — so we build for durability, compliance and long-term returns.",
        "p2": "Our team manages the full lifecycle: planning, structural engineering, procurement, execution and handover — with disciplined timelines and transparent budgeting at every stage.",
        "highlights": ["Structural engineering to commercial codes", "Disciplined project timelines", "Transparent, itemised budgeting", "Quality checks at every milestone"],
        "offers": [
            ("Retail & Showroom Spaces", "High-visibility, footfall-ready builds designed to attract and serve customers."),
            ("Office Buildings", "Functional, professional workspaces built for productivity and scale."),
            ("Mixed-Use Developments", "Integrated commercial-cum-residential projects delivered end to end."),
            ("Turnkey Execution", "A single accountable team from foundation to final handover."),
        ],
    },
    {
        "slug": "residential-project-construction", "cat": "construction",
        "name": "Residential Project Construction",
        "img": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=80",
        "intro": "Homes and residential developments crafted for comfort, durability and everyday living.",
        "p1": "Whether it's an independent house or a residential development, we build homes that families are proud to live in. Quality materials, sound engineering and careful workmanship come together to create spaces that are safe, comfortable and built to stand the test of time.",
        "p2": "We keep you informed and involved throughout — with clear timelines, honest pricing and a finish that matches the vision you started with.",
        "highlights": ["Quality materials & workmanship", "Vaastu-friendly planning on request", "Clear stage-wise updates", "Built for long-term durability"],
        "offers": [
            ("Independent Houses", "Custom-built homes designed around how your family lives."),
            ("Residential Layouts", "Planned residential developments with quality infrastructure."),
            ("Renovation & Rebuild", "Modernising or rebuilding existing homes to new standards."),
            ("Turnkey Delivery", "One team handling everything from design to keys in hand."),
        ],
    },
    {
        "slug": "apartments-construction", "cat": "construction",
        "name": "Apartments Construction",
        "img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",
        "intro": "Multi-storey apartment buildings engineered for modern community living and long-term value.",
        "p1": "We construct apartment buildings that balance efficient design, structural integrity and quality living. From compact urban blocks to larger residential towers, every project is engineered for safety, comfort and lasting value.",
        "p2": "Smart space planning, reliable common amenities and quality finishes make our apartments a sound choice for both residents and investors.",
        "highlights": ["Earthquake-resistant structural design", "Efficient space & amenity planning", "Quality common-area finishes", "On-time, milestone-based delivery"],
        "offers": [
            ("Residential Towers", "Multi-storey buildings built for community living and value."),
            ("Compact Apartment Blocks", "Efficient, well-planned blocks for urban locations."),
            ("Amenity Integration", "Lifts, parking, common areas and utilities done right."),
            ("Investor-Ready Builds", "Quality construction that protects long-term value."),
        ],
    },

    # ---------------- INTERIOR DESIGN ----------------
    {
        "slug": "office-interior", "cat": "interior",
        "name": "Office Interior",
        "img": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "intro": "Productive, professional workspaces that reflect your brand and inspire your team.",
        "p1": "Your office says a lot about your business. We design workspaces that are functional and beautiful — optimising layout, lighting, acoustics and storage to help your team do their best work while impressing every visitor.",
        "p2": "From workstations and cabins to boardrooms and reception areas, we deliver complete, turnkey office interiors tailored to your brand and budget.",
        "highlights": ["Ergonomic, productive layouts", "Brand-aligned design language", "Smart lighting & acoustics", "Turnkey execution"],
        "offers": [
            ("Workstations & Cabins", "Efficient, comfortable setups that maximise usable space."),
            ("Boardrooms & Meeting Rooms", "Professional spaces built for focus and collaboration."),
            ("Reception & Lounge", "Welcoming front-of-house areas that make an impression."),
            ("Space Planning", "Layouts that get the most from every square foot."),
        ],
    },
    {
        "slug": "residential-interior", "cat": "interior",
        "name": "Residential Interior",
        "img": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=80",
        "intro": "Complete home interiors designed cohesively, room by room, for comfort and style.",
        "p1": "We transform houses into homes with interiors designed around your lifestyle, taste and budget. From concept to the final styling touch, our designers create cohesive spaces where every room flows beautifully into the next.",
        "p2": "Colour, texture, lighting, furniture and finishes — we handle it all, delivering a home that feels uniquely yours.",
        "highlights": ["Personalised design concepts", "Cohesive whole-home styling", "Quality materials & finishes", "End-to-end project management"],
        "offers": [
            ("Full Home Design", "A unified look and feel across every room in your home."),
            ("Bedrooms", "Restful, well-organised private spaces designed for comfort."),
            ("Storage & Wardrobes", "Smart, custom storage tailored to your needs."),
            ("Styling & Finishing", "The final details that bring a home to life."),
        ],
    },
    {
        "slug": "kitchen-interior", "cat": "interior",
        "name": "Kitchen Interior",
        "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=1200&q=80",
        "intro": "Modular, ergonomic kitchens that combine smart storage, durability and beautiful finishes.",
        "p1": "The kitchen is the heart of the home. We design modular kitchens that are as practical as they are stunning — with efficient work triangles, ample storage and materials that stand up to daily use.",
        "p2": "From layout and cabinetry to countertops and appliances, we deliver a kitchen tailored to how you cook and live.",
        "highlights": ["Ergonomic work-triangle layouts", "Moisture & heat-resistant materials", "Maximised, smart storage", "Premium fittings & finishes"],
        "offers": [
            ("Modular Kitchens", "Configurable, factory-finished cabinetry for a flawless look."),
            ("Countertops & Backsplash", "Durable, easy-to-clean surfaces in the finish you love."),
            ("Smart Storage", "Pull-outs, corner units and organisers that use every inch."),
            ("Appliance Integration", "Seamlessly built-in appliances for a clean finish."),
        ],
    },
    {
        "slug": "living-room-interior", "cat": "interior",
        "name": "Living Room Interior",
        "img": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=80",
        "intro": "Inviting living spaces with the right balance of layout, lighting, furniture and finishes.",
        "p1": "Your living room is where life happens — so we design it to be welcoming, comfortable and effortlessly stylish. We balance seating, lighting, storage and decor to create a space that works for both everyday living and entertaining.",
        "p2": "Whether your taste is modern, classic or somewhere in between, we craft a living room that reflects your personality.",
        "highlights": ["Balanced, functional layouts", "Layered lighting design", "Feature walls & TV units", "Coordinated furniture & decor"],
        "offers": [
            ("Seating & Layout", "Comfortable arrangements that suit your space and lifestyle."),
            ("Feature & TV Walls", "Statement walls and media units that anchor the room."),
            ("Lighting Design", "Ambient, task and accent lighting done right."),
            ("Decor & Styling", "Finishing touches that pull the whole look together."),
        ],
    },
    {
        "slug": "balcony-designing", "cat": "interior",
        "name": "Balcony Designing",
        "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "intro": "Balconies reimagined as relaxing, functional extensions of your living space.",
        "p1": "Don't let your balcony go to waste. We turn balconies into beautiful, usable spaces — cosy sit-outs, green corners or stylish lounge areas that bring the outdoors into your daily life.",
        "p2": "With weather-suitable materials, smart seating and greenery, we design balconies that are as durable as they are inviting.",
        "highlights": ["Weather-resistant materials", "Space-smart seating", "Greenery & vertical gardens", "Mood lighting"],
        "offers": [
            ("Sit-Out Corners", "Comfortable nooks perfect for morning coffee or unwinding."),
            ("Green Balconies", "Planters and vertical gardens that bring nature closer."),
            ("Flooring & Railings", "Durable, stylish finishes suited to outdoor exposure."),
            ("Ambient Lighting", "Warm lighting that transforms the space after dark."),
        ],
    },

    # ---------------- PROPERTY SALES ----------------
    {
        "slug": "residential-buildings", "cat": "property",
        "name": "Residential Buildings",
        "img": "https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=1200&q=80",
        "intro": "Ready and upcoming residential buildings in prime, well-connected locations.",
        "p1": "Looking for a residential building to buy or invest in? We offer a curated selection of quality residential properties in sought-after locations, each with verified documentation and transparent pricing.",
        "p2": "Our advisors help you compare options, understand the paperwork and make a confident decision that fits your needs and budget.",
        "highlights": ["Verified, clear-title properties", "Prime, well-connected locations", "Transparent pricing", "End-to-end paperwork support"],
        "offers": [
            ("Ready-to-Move Buildings", "Move in without the wait, with full documentation in place."),
            ("Under-Construction Options", "Get in early on upcoming residential projects."),
            ("Investment Guidance", "Advice on locations and returns that match your goals."),
            ("Documentation Support", "We handle the legwork so the process stays simple."),
        ],
    },
    {
        "slug": "commercial-buildings", "cat": "property",
        "name": "Commercial Buildings",
        "img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
        "intro": "Offices, retail and business premises ideal for investment or operations.",
        "p1": "From office blocks to retail buildings, we help you find or sell commercial property that delivers value. Every listing is location-assessed and document-verified, so you can invest or operate with confidence.",
        "p2": "Whether you're expanding your business or building a property portfolio, our team guides you to the right commercial opportunity.",
        "highlights": ["High-footfall & business locations", "Document-verified listings", "Investment & yield guidance", "Negotiation & paperwork support"],
        "offers": [
            ("Office Buildings", "Professional premises ready for business or leasing."),
            ("Retail Buildings", "High-visibility spaces built for commercial success."),
            ("Investment Assets", "Income-generating commercial property options."),
            ("Advisory Support", "Guidance on value, yield and documentation."),
        ],
    },
    {
        "slug": "individual-houses", "cat": "property",
        "name": "Individual Houses",
        "img": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=1200&q=80",
        "intro": "Independent homes and villas offering privacy, space and long-term value.",
        "p1": "Prefer a home of your own with no shared walls? We offer independent houses and villas that combine privacy, space and comfort — in locations that suit your lifestyle and budget.",
        "p2": "From compact independent homes to spacious villas, our advisors help you find the right property and complete the purchase smoothly.",
        "highlights": ["Independent, private living", "Verified ownership documents", "Range of sizes & budgets", "Smooth purchase process"],
        "offers": [
            ("Independent Houses", "Standalone homes offering space and privacy."),
            ("Villas", "Premium homes with generous space and amenities."),
            ("Gated Community Homes", "Independent living with community security and facilities."),
            ("Buyer Guidance", "Support through selection, pricing and paperwork."),
        ],
    },
    {
        "slug": "apartment-flats", "cat": "property",
        "name": "Apartment Flats",
        "img": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
        "intro": "1, 2 & 3 BHK flats across trusted projects to suit every budget.",
        "p1": "Apartments offer convenience, community and value. We list quality flats across trusted projects — from compact 1 BHKs to spacious 3 BHKs — each with verified paperwork and honest pricing.",
        "p2": "Tell us your budget and preferred location, and we'll shortlist the best options and guide you through to purchase.",
        "highlights": ["1, 2 & 3 BHK options", "Trusted, quality projects", "Amenity-rich communities", "Transparent pricing & paperwork"],
        "offers": [
            ("1 BHK Flats", "Compact, efficient homes ideal for singles and starters."),
            ("2 BHK Flats", "Comfortable family homes with balanced space."),
            ("3 BHK Flats", "Spacious apartments for growing families."),
            ("Purchase Support", "Guidance from shortlisting to final registration."),
        ],
    },
    {
        "slug": "open-plots", "cat": "property",
        "name": "Open Plots",
        "img": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=80",
        "intro": "Clear-title residential and layout plots ready to build on or hold as investment.",
        "p1": "Buying land is one of the safest long-term investments. We offer clear-title open plots in approved layouts and growing locations — perfect for building your dream home or holding for appreciation.",
        "p2": "Every plot is verified for title, approvals and access, so you invest with complete peace of mind.",
        "highlights": ["Clear-title, approved layouts", "Growth-corridor locations", "Verified access & boundaries", "Investment & resale guidance"],
        "offers": [
            ("Residential Plots", "Build-ready plots in planned, approved layouts."),
            ("Layout Plots", "Well-planned plots with proper infrastructure."),
            ("Investment Plots", "Land in high-appreciation growth corridors."),
            ("Title Verification", "Full checks on ownership, approvals and access."),
        ],
    },
    {
        "slug": "agriculture-lands", "cat": "property",
        "name": "Agriculture Lands",
        "img": "https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?auto=format&fit=crop&w=1200&q=80",
        "intro": "Fertile agricultural land parcels with verified documentation and access.",
        "p1": "We deal in agricultural land parcels suited for farming, plantation or long-term investment. Each parcel is checked for title, water access and connectivity so you can buy with confidence.",
        "p2": "Whether for cultivation or as a strategic land holding, our team helps you find and secure the right piece of land.",
        "highlights": ["Fertile, cultivable parcels", "Verified title & documentation", "Water & road access checked", "Investment guidance"],
        "offers": [
            ("Farm Land", "Cultivable parcels suited for agriculture and plantation."),
            ("Investment Land", "Strategically located holdings for long-term value."),
            ("Water & Access Checks", "Verified irrigation and connectivity."),
            ("Documentation Support", "Guidance through title and registration."),
        ],
    },
    {
        "slug": "commercial-space", "cat": "property",
        "name": "Commercial Space",
        "img": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80",
        "intro": "Shops, showrooms and office spaces for lease or purchase in high-footfall areas.",
        "p1": "The right commercial space can make a business. We offer shops, showrooms and office spaces in prime, high-footfall locations — available for purchase or lease, with verified paperwork throughout.",
        "p2": "From a single retail unit to a full office floor, our advisors match you with the space that fits your business and budget.",
        "highlights": ["High-footfall prime locations", "Purchase or lease options", "Verified documentation", "Business-fit advisory"],
        "offers": [
            ("Retail Shops", "Street-facing, high-visibility units for retail."),
            ("Showrooms", "Large-format spaces built to showcase products."),
            ("Office Spaces", "Ready commercial floors for teams of any size."),
            ("Lease & Buy Support", "Guidance and paperwork for either route."),
        ],
    },
]

# ---------- Shared building blocks ----------

def topbar():
    return '''  <div class="topbar">
    <div class="container">
      <div class="tb-left">
        <a href="tel:+919959802777"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>+91 99598 02777</a>
        <a href="mailto:rvrrservice.llp@gmail.com"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v16H4z"/><path d="m22 6-10 7L2 6"/></svg>rvrrservice.llp@gmail.com</a>
      </div>
      <div class="tb-right">
        <a href="contact.html">Get a Quote</a>
        <a href="about.html">About Us</a>
      </div>
    </div>
  </div>'''

def header():
    return '''  <header class="header">
    <div class="container nav">
      <a href="index.html" class="logo">
        <img src="images/logo.jpg" alt="RVRR Construction &amp; Property Sales" class="logo-img" width="600" height="403" />
      </a>
      <nav>
        <ul class="nav-links">
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About Us</a></li>
          <li><a href="services.html" class="active">Our Services</a></li>
          <li><a href="contact.html">Contact Us</a></li>
          <li class="nav-cta"><a href="contact.html" class="btn btn-primary">Enquire Now</a></li>
        </ul>
      </nav>
      <button class="hamburger" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </header>'''

def footer():
    return '''  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a href="index.html" class="logo">
            <img src="images/logo.jpg" alt="RVRR Construction &amp; Property Sales" class="logo-img" width="600" height="403" />
          </a>
          <p>Your trusted partner for construction, interior design and property sales — building spaces and shaping lifestyles with integrity.</p>
          <div class="socials">
            <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12z"/></svg></a>
            <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>
            <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0zM.5 8h4V24h-4V8zM8 8h3.8v2.2h.05c.53-1 1.83-2.2 3.77-2.2 4.03 0 4.78 2.65 4.78 6.1V24h-4v-6.9c0-1.65-.03-3.77-2.3-3.77-2.3 0-2.65 1.8-2.65 3.65V24H8V8z"/></svg></a>
            <a href="https://wa.me/919959802777" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.3 4.7 4.8-1.3A10 10 0 1 0 12 2zm5.5 14.1c-.2.6-1.2 1.2-1.7 1.2-.4 0-.9.1-3-1s-3.6-3.5-3.7-3.7-.9-1.2-.9-2.3.6-1.6.8-1.8.4-.3.6-.3h.5c.2 0 .4 0 .6.5s.7 1.7.7 1.8.1.3 0 .5-.1.3-.3.5-.3.4-.4.5-.3.3-.1.6.5.9 1.1 1.5c.8.7 1.4.9 1.7 1s.4.1.6-.1.7-.8.9-1.1.4-.2.6-.1 1.5.7 1.7.8.4.2.5.3 0 .6-.2 1.2z"/></svg></a>
          </div>
        </div>
        <div>
          <h4>Quick Links</h4>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="about.html">About Us</a></li>
            <li><a href="services.html">Our Services</a></li>
            <li><a href="contact.html">Contact Us</a></li>
          </ul>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="services.html#construction">Construction</a></li>
            <li><a href="services.html#interior">Interior Design</a></li>
            <li><a href="services.html#property">Property Sales</a></li>
            <li><a href="contact.html">Get a Quote</a></li>
          </ul>
        </div>
        <div>
          <h4>Get in Touch</h4>
          <ul class="f-contact">
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><span>H No 20-1392, Papireddy Colony,<br />Chandanagar, Serilingampally,<br />Hyderabad, Telangana - 500019</span></li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg><a href="tel:+919959802777">+91 99598 02777</a></li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v16H4z"/><path d="m22 6-10 7L2 6"/></svg><a href="mailto:rvrrservice.llp@gmail.com">rvrrservice.llp@gmail.com</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span id="year">2026</span> RVRR Construction &amp; Property Sales. All rights reserved.</span>
        <span>Built with care &middot; Designed for clarity</span>
      </div>
    </div>
  </footer>

  <!-- MOBILE FOOTER MENU (5 Key Pages) -->
  <nav class="mobile-footer-menu" aria-label="Mobile Navigation">
    <a href="index.html" class="mfm-item" data-page="home">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9.5L12 3l9 6.5V20a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9.5z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      <span>Home</span>
    </a>
    <a href="services.html" class="mfm-item" data-page="services">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="9" y1="6" x2="9" y2="6.01"/><line x1="15" y1="6" x2="15" y2="6.01"/><line x1="9" y1="10" x2="9" y2="10.01"/><line x1="15" y1="10" x2="15" y2="10.01"/><line x1="9" y1="14" x2="9" y2="14.01"/><line x1="15" y1="14" x2="15" y2="14.01"/><path d="M10 22v-4h4v4"/></svg>
      <span>Services</span>
    </a>
    <a href="services.html#property" class="mfm-item" data-page="property">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a7.5 7.5 0 0 0-7.5 7.5c0 5.25 7.5 12.5 7.5 12.5s7.5-7.25 7.5-12.5A7.5 7.5 0 0 0 12 2z"/><circle cx="12" cy="9.5" r="2.5"/></svg>
      <span>Properties</span>
    </a>
    <a href="about.html" class="mfm-item" data-page="about">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      <span>About</span>
    </a>
    <a href="contact.html" class="mfm-item" data-page="contact">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
      <span>Contact</span>
    </a>
  </nav>'''


ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'

def build_page(svc):
    cat = CATEGORIES[svc["cat"]]
    # highlights
    hl = "\n".join('            <li>{}</li>'.format(h) for h in svc["highlights"])
    # offer cards
    offer_cards = "\n".join(
        '''        <div class="sub-card reveal">
          <div class="ci">{icon}</div>
          <h4>{t}</h4>
          <p>{d}</p>
        </div>'''.format(icon=cat["icon"], t=t, d=d) for (t, d) in svc["offers"]
    )
    # related (siblings in same category, excluding self) - up to 3
    siblings = [s for s in SERVICES if s["cat"] == svc["cat"] and s["slug"] != svc["slug"]][:3]
    related_cards = "\n".join(
        '''        <a href="service-{slug}.html" class="sub-card reveal" style="display:block;">
          <div class="ci">{icon}</div>
          <h4>{name}</h4>
          <p>{intro}</p>
          <span class="link" style="color:var(--accent);font-weight:700;">Explore {arrow}</span>
        </a>'''.format(slug=s["slug"], icon=cat["icon"], name=s["name"], intro=s["intro"], arrow=ARROW)
        for s in siblings
    )

    # ---- SEO: canonical, keywords, Open Graph, Twitter ----
    url = "{}/service-{}.html".format(BASE, svc["slug"])
    ogimg = svc["img"]
    keywords = "{n}, {n} services, {n} company, {catkw}, RVRR construction & property sales".format(
        n=svc["name"], catkw=cat["kw"])
    seo_meta = '''  <meta name="keywords" content="{kw}" />
  <meta name="author" content="RVRR Construction & Property Sales" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="theme-color" content="#2b2e31" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png" />
  <link rel="shortcut icon" href="favicon.ico" />
  <link rel="manifest" href="site.webmanifest" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="RVRR Construction & Property Sales" />
  <meta property="og:locale" content="en_IN" />
  <meta property="og:title" content="{name} | RVRR Construction & Property Sales" />
  <meta property="og:description" content="{intro}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{ogimg}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{name} | RVRR Construction & Property Sales" />
  <meta name="twitter:description" content="{intro}" />
  <meta name="twitter:image" content="{ogimg}" />'''.format(
        kw=keywords, url=url, name=svc["name"], intro=svc["intro"], ogimg=ogimg)

    # ---- SEO: JSON-LD structured data (Service + BreadcrumbList) ----
    service_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": svc["name"], "serviceType": svc["name"], "url": url,
        "description": svc["intro"], "category": cat["name"], "areaServed": "IN",
        "provider": {
            "@type": ["GeneralContractor", "RealEstateAgent"],
            "name": "RVRR Construction & Property Sales",
            "url": BASE + "/", "telephone": "+91-99598-02777",
            "email": "rvrrservice.llp@gmail.com",
        },
    }
    breadcrumb_ld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/index.html"},
            {"@type": "ListItem", "position": 2, "name": cat["name"], "item": BASE + "/services.html"},
            {"@type": "ListItem", "position": 3, "name": svc["name"], "item": url},
        ],
    }
    jsonld = ('  <script type="application/ld+json">\n  ' + json.dumps(service_ld) +
              '\n  </script>\n  <script type="application/ld+json">\n  ' +
              json.dumps(breadcrumb_ld) + '\n  </script>')

    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} | RVRR Construction &amp; Property Sales</title>
  <meta name="description" content="{intro}" />
{seo_meta}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/style.css?v=4" />
{jsonld}
</head>
<body>

{topbar}

{header}

  <!-- PAGE BANNER -->
  <section class="page-banner" id="main-content" role="main" aria-label="{name}" style="background:linear-gradient(120deg, rgba(31,33,36,0.90), rgba(43,46,49,0.78)), url('{img}') center/cover no-repeat;">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb" style="margin-bottom:10px;"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="{anchor}">{cat_name}</a> &nbsp;/&nbsp; <span>{name}</span></nav>
      <h1>{name}</h1>
    </div>
  </section>

  <!-- OVERVIEW -->
  <section class="section">
    <div class="container">
      <div class="split">
        <div class="media reveal">
          <img src="{img}" alt="{name} by RVRR Construction &amp; Property Sales" width="1200" height="800" loading="lazy" decoding="async" />
        </div>
        <div class="reveal">
          <span class="eyebrow">{cat_name}</span>
          <h2>{name}</h2>
          <p>{p1}</p>
          <p>{p2}</p>
          <ul class="check-list">
{highlights}
          </ul>
          <a href="contact.html" class="btn btn-primary">Enquire About This Service {arrow}</a>
        </div>
      </div>
    </div>
  </section>

  <!-- WHAT WE OFFER -->
  <section class="section bg-muted">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">What We Offer</span>
        <h2>{name} — the details</h2>
        <p>Here's what's included when you work with RVRR for {name_lower}.</p>
      </div>
      <div class="sub-grid">
{offer_cards}
      </div>
    </div>
  </section>

  <!-- RELATED -->
  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">More in {cat_name}</span>
        <h2>Related services</h2>
        <p>Explore other services within our {cat_name} line.</p>
      </div>
      <div class="sub-grid">
{related_cards}
      </div>
      <div class="text-center" style="margin-top:40px;">
        <a href="services.html" class="btn btn-outline">View All Services</a>
      </div>
    </div>
  </section>

  <!-- CTA BAND -->
  <section class="section-sm">
    <div class="container">
      <div class="cta-band reveal">
        <div>
          <h2>Interested in {name}?</h2>
          <p>Tell us your requirement and our team will get back to you with the right solution and a free estimate.</p>
        </div>
        <a href="contact.html" class="btn btn-light">Get a Free Quote {arrow}</a>
      </div>
    </div>
  </section>

{footer}

  <script src="js/main.js?v=4"></script>
</body>
</html>
'''.format(
        name=svc["name"], name_lower=svc["name"].lower(), intro=svc["intro"],
        img=svc["img"], anchor=cat["anchor"], cat_name=cat["name"],
        p1=svc["p1"], p2=svc["p2"], highlights=hl, offer_cards=offer_cards,
        related_cards=related_cards, arrow=ARROW,
        topbar=topbar(), header=header(), footer=footer(),
        seo_meta=seo_meta, jsonld=jsonld,
    )


def main():
    count = 0
    for svc in SERVICES:
        html = build_page(svc)
        path = os.path.join(OUT_DIR, "service-{}.html".format(svc["slug"]))
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print("Generated service-{}.html".format(svc["slug"]))
    print("\nDone. {} service pages generated.".format(count))


if __name__ == "__main__":
    main()
