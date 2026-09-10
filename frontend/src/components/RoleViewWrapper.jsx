import React from 'react';

export default function RoleViewWrapper({ currentRole, allowedRoles, children }) {
  if (!allowedRoles.includes(currentRole)) {
    return null;
  }
  return <>{children}</>;
}
