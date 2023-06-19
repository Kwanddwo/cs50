describe('Trivia working as expected', () => {
  beforeEach(() => {
    cy.visit('http://trivia/')
  })

    context('Multiple choice', () => {
      it('Works correctly on clicking the correct button', () => {
        const truebutton = cy.getByData('correctbutton')
        truebutton.click().should('have.css', 'background-color', 'rgb(126, 255, 115)')
        cy.contains("Correct!")
      })
  
      it('Works correctly when clicking the wrong button', () => {
        const falsebutton = cy.getByData('falsebutton')
        falsebutton.click({multiple : true}).should('have.css', 'background-color', 'rgb(252, 146, 146)')
        cy.contains("Incorrect")
      })
    })

    context('Unique choice', () => {
      it('Works when inputting correct answer', () => {
        cy.get('#q2field').type('MoRoCco')
        cy.contains("Check Answer").click()
        cy.get('#q2field').should('have.css', 'background-color', 'rgb(126, 255, 115)')
        cy.contains("Correct!")
      })
  
      it('Works when inputting wrong answer', () => {
        cy.get('#q2field').type('Mozambique')
        cy.contains("Check Answer").click()
        cy.get('#q2field').should('have.css', 'background-color', 'rgb(252, 146, 146)')
        cy.contains("Incorrect")
      })
    })
})