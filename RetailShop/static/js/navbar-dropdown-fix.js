// Script pour corriger les problèmes de dropdown dans la navbar
$(document).ready(function() {
    // S'assurer que Bootstrap dropdowns sont initialisés
    $('.dropdown-toggle').dropdown();
    
    // Correction pour les dropdowns sur desktop avec hover
    if ($(window).width() > 767) {
        $('.navbar .dropdown').hover(
            function() {
                // Montrer le dropdown au hover
                $(this).addClass('show');
                $(this).find('.dropdown-menu').addClass('show');
                $(this).find('.dropdown-toggle').attr('aria-expanded', 'true');
            },
            function() {
                // Cacher le dropdown quand on sort
                $(this).removeClass('show');
                $(this).find('.dropdown-menu').removeClass('show');
                $(this).find('.dropdown-toggle').attr('aria-expanded', 'false');
            }
        );
    }
    
    // Gérer les clics sur mobile
    $('.navbar .dropdown-toggle').on('click', function(e) {
        if ($(window).width() <= 767) {
            e.preventDefault();
            const $dropdown = $(this).parent();
            const $menu = $(this).next('.dropdown-menu');
            
            if ($dropdown.hasClass('show')) {
                $dropdown.removeClass('show');
                $menu.removeClass('show');
                $(this).attr('aria-expanded', 'false');
            } else {
                // Fermer les autres dropdowns ouverts
                $('.navbar .dropdown').removeClass('show');
                $('.navbar .dropdown-menu').removeClass('show');
                $('.navbar .dropdown-toggle').attr('aria-expanded', 'false');
                
                // Ouvrir celui-ci
                $dropdown.addClass('show');
                $menu.addClass('show');
                $(this).attr('aria-expanded', 'true');
            }
        }
    });
    
    // Fermer le dropdown en cliquant ailleurs
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.dropdown').length) {
            $('.navbar .dropdown').removeClass('show');
            $('.navbar .dropdown-menu').removeClass('show');
            $('.navbar .dropdown-toggle').attr('aria-expanded', 'false');
        }
    });
    
    // Gérer le redimensionnement de la fenêtre
    $(window).on('resize', function() {
        if ($(window).width() > 767) {
            // Réactiver le hover pour desktop
            $('.navbar .dropdown').off('click');
        } else {
            // Désactiver le hover pour mobile
            $('.navbar .dropdown').off('mouseenter mouseleave');
        }
    });
});
