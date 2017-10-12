import React from 'react';
import PlayerLink from '../static/teams.jsx';
import { mount } from 'enzyme';

test('PlayerLink', () => {
	// const username = "Test user";
	// const friend = false;
	const wrapper = mount(
    <ContentBox/>
	);
	const p = wrapper.find('#content');
  	expect(p.text()).toBe('Test user');
});



describe('Addition', () => {
  it('knows that 2 and 2 make 4', () => {
    expect(2 + 2).toBe(4);
  });
});
